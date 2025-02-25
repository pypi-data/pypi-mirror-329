from dataclasses import dataclass
from typing import List
import base64

from google.cloud import firestore
from pxr import Sdf

from zeta.db import BaseData, NestedZetaBase
from zeta.usd.sync import SyncData, SyncOp, SyncOpList, SyncOpType
from zeta.utils.logging import zetaLogger


@dataclass
class ZetaLayerData(BaseData):
    data: dict


class ZetaLayer(NestedZetaBase):
    def __init__(self):
        super().__init__()
        self._layer: Sdf.Layer = None
        self._listener = None

    @property
    def collection_name(self) -> str:
        return "layers"

    @property
    def parent_uid_field(cls) -> str:
        return "session_uid"

    @property
    def data_class(self):
        return ZetaLayerData

    @property
    def layer(self) -> Sdf.Layer:
        return self._layer

    def _get_sync_data(self) -> SyncData:
        if self._data is None:
            raise ValueError("ZetaLayerData is None")

        sync_data = SyncData.CreateNew()

        if self._data.data is None:
            # When data is missing, return an empty SyncData
            return sync_data

        for node_path, node_data in self._data.data.items():
            sync_data.CreateNode(node_path, node_data["nodeType"])
            for field_name, field_value in node_data["fields"].items():
                if isinstance(field_value, bytes):
                    encoded_value = base64.b64encode(field_value)
                elif isinstance(field_value, str):
                    encoded_value = field_value
                else:
                    raise ValueError(f"Unknown field value type: {type(field_value)}")
                sync_data.SetField(node_path, field_name, encoded_value)

        return sync_data

    def _get_layer_update_data(self, ops: List[SyncOp]):
        layer_update = {}
        for sync_op in ops:
            if sync_op.opType == SyncOpType.CreateNode:
                node_path: str = sync_op.nodePath
                node_type: int = sync_op.nodeType
                if (node_path in layer_update):
                    zetaLogger.warning(f"Found duplicate node path: {node_path}")
                else:
                    layer_update[node_path] = {
                        "nodeType": node_type,
                        "fields": {},
                    }

            elif sync_op.opType == SyncOpType.SetField:
                node_path: str = sync_op.nodePath
                field_name: str = sync_op.fieldName
                field_value: bytearray = sync_op.GetFieldValue()
                if node_path not in layer_update:
                    layer_update[node_path] = {
                        "fields": {}
                    }
                layer_update[node_path]["fields"][field_name] = bytes(field_value)

            elif sync_op.opType == SyncOpType.MoveNode:
                raise NotImplementedError("MoveNode not implemented")

            elif sync_op.opType == SyncOpType.EraseNode:
                node_path: str = sync_op.nodePath
                layer_update[node_path] = firestore.DELETE_FIELD

            elif sync_op.opType == SyncOpType.EraseField:
                node_path: str = sync_op.nodePath
                field_name: str = sync_op.fieldName

                if node_path not in layer_update:
                    layer_update[node_path] = {
                        "fields": {}
                    }

                layer_update[node_path]["fields"][field_name] = firestore.DELETE_FIELD

            else:
                zetaLogger.warning(f"Unknown SyncOpType: {sync_op.opType}")

        return layer_update

    def load_layer(self) -> Sdf.Layer:
        self._layer = Sdf.Layer.CreateAnonymous(f"layer-{self._data.uid}.zeta")

        # Pull layer updates from DB automatically when loading the layer for the first time.
        self.pull_updates()

        return self._layer

    def pull_updates(self):
        sync_data: SyncData = self._get_sync_data()
        SyncData.RefreshData(self._layer, sync_data)

    def push_updates(self):
        ops: SyncOpList = SyncData.GetLayerUpdates(self._layer)
        layer_data_update = self._get_layer_update_data(ops)

        if len(layer_data_update) == 0:
            # Explicitly return here to avoid updating the layer data with an empty update.
            return

        layer_update = {
            "data": layer_data_update,
            "updatedAt": self._get_current_time(),
        }

        # Use set(merge=True) instead of update() to carry out a deep update.
        self._ref.set(layer_update, merge=True)
