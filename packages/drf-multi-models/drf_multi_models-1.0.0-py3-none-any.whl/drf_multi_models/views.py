from typing import List

from rest_framework.renderers import BaseRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView


class MultiModelAPIView(APIView):
    """Implementation of APIView for MultiModel."""

    def get_renderers(self) -> List[BaseRenderer]:
        """Overrides the DRF APIView's get_renderers method to remove the BrowsableAPIRenderer."""
        # TODO: Need to implement a functional `BrowsableAPIRenderer` for MultiModel
        renderer_classes = [
            renderer_class
            for renderer_class in self.renderer_classes
            if renderer_class != BrowsableAPIRenderer
        ]
        return [renderer() for renderer in renderer_classes]
