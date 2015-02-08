from django.utils.translation import ugettext as _
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.asset.models import AssetType, DELETED, LIVE, Assets
from apps.asset.serializers import AssetTypeSerializer, AssetSerializer
from apps.authentication.custom_permission_drf import AssetAccessPermission
from apps.resorts.models import ResortLocation
from apps.resorts.utils import get_resort_for_user


class AssetViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, AssetAccessPermission]

    def create(self, request):
        resort = get_resort_for_user(request.user)
        asset_type_id = request.data.get('asset_type_id', '')
        location_id = request.data.get('location_id', '')

        if asset_type_id:
            try:
                asset_type = AssetType.objects.get(asset_type_id=asset_type_id)
                if asset_type.asset_type_status == DELETED:
                    return Response({_('detail'): _('asset_type not found')}, status=400)
            except:
                return Response({_('detail'): _('asset_type not found')}, status=400)
        else:
            return Response({_('detail'): _('asset_type_id not provided')}, status=400)

        if location_id:
            try:
                location = ResortLocation.objects.get(location_id=location_id)
                if location.location_status == DELETED:
                    return Response({_('detail'): _('location not found')}, status=400)
            except:
                return Response({_('detail'): _('location not found')}, status=400)
        else:
            return Response({_('detail'): _('location_id not provided')}, status=400)

        asset_data = AssetSerializer(data=request.data, fields='asset_name')

        if asset_data.is_valid():
            asset = asset_data.save(location=location, asset_type=asset_type, resort=resort)
        else:
            return Response(asset_data.errors, status=400)

        return Response(AssetSerializer(asset).data, status=200)

    def update(self, request, pk=None):

        try:
            asset = Assets.objects.get(asset_id=pk)
            if asset.asset_status == DELETED:
                return Response({_('detail'): _('asset not found')}, status=400)
        except:
            return Response({_('detail'): _('asset not found')}, status=400)

        asset_type_id = request.data.get('asset_type_id', '')
        location_id = request.data.get('location_id', '')
        asset_type = None
        location = None

        if asset_type_id:
            try:
                asset_type = AssetType.objects.get(asset_type_id=asset_type_id)
                if asset_type.asset_type_status == DELETED:
                    return Response({_('detail'): _('asset_type not found')}, status=400)
            except:
                return Response({_('detail'): _('asset_type not found')}, status=400)

        if location_id:
            try:
                location = ResortLocation.objects.get(location_id=location_id)
                if location.location_status == DELETED:
                    return Response({_('detail'): _('location not found')}, status=400)
            except:
                return Response({_('detail'): _('location not found')}, status=400)

        asset_data = AssetSerializer(asset, data=request.data, fields='asset_name')

        if asset_data.is_valid():
            if (asset_type is not None) and (location is not None):
                asset = asset_data.save(asset_type=asset_type, location=location)
            elif asset_type is not None:
                asset = asset_data.save(asset_type=asset_type)
            elif location is not None:
                asset = asset_data.save(location=location)
            else:
                asset = asset_data.save()
        else:
            return Response(asset_data.errors, status=400)

        return Response(AssetSerializer(asset).data, status=200)

    def retrieve(self, request, pk=None):
        try:
            asset = Assets.objects.get(asset_id=pk)
            if asset.asset_status == DELETED:
                return Response({_('detail'): _('asset not found')}, status=400)
        except:
            return Response({_('detail'): _('asset not found')}, status=400)

        return Response(AssetSerializer(asset).data, status=200)

    def destroy(self, request, pk=None):
        try:
            asset = Assets.objects.get(asset_id=pk)
            if asset.asset_status == DELETED:
                return Response({_('detail'): _('asset not found')}, status=400)
        except:
            return Response({_('detail'): _('asset not found')}, status=400)

        asset.asset_status = DELETED
        asset.save()

        return Response({
            "asset_id": asset.asset_id,
            "status": "deleted"
        }, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        search = request.query_params.get('search', '')
        location_id = request.query_params.get('area_id', '')
        asset_type_id = request.query_params.get('asset_type_id', '')
        order_by = request.query_params.get('order_by', 'asset_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        if asset_type_id:
            try:
                asset_type = AssetType.objects.get(asset_type_id=asset_type_id)
                if asset_type.asset_type_status == DELETED:
                    return Response({_('detail'): _('asset_type not found')}, status=400)
            except:
                return Response({_('detail'): _('asset_type not found')}, status=400)

        if location_id:
            try:
                location = ResortLocation.objects.get(location_id=location_id)
                if location.location_status == DELETED:
                    return Response({_('detail'): _('location not found')}, status=400)
            except:
                return Response({_('detail'): _('location not found')}, status=400)

        if location_id and asset_type_id:
            query = Assets.objects.filter(asset_name__icontains=search, resort=resort, asset_status=LIVE,
                                          asset_type=asset_type, location=location).order_by(order)
        elif location_id:
            query = Assets.objects.filter(asset_name__icontains=search, resort=resort, asset_status=LIVE,
                                          location=location).order_by(order)
        elif asset_type_id:
            query = Assets.objects.filter(asset_name__icontains=search, resort=resort, asset_status=LIVE,
                                          asset_type=asset_type).order_by(order)
        else:
            query = Assets.objects.filter(asset_name__icontains=search, resort=resort, asset_status=LIVE) \
                .order_by(order)

        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AssetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AssetTypeViewSet(ViewSet, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, AssetAccessPermission]

    # def create(self, request):
    #     resort = get_resort_for_user(request.user)
    #
    #     asset_type_data = AssetTypeSerializer(data=request.data, fields='asset_type_name')
    #
    #     if asset_type_data.is_valid():
    #         asset_type = asset_type_data.save(resort=resort)
    #     else:
    #         return Response(asset_type_data.errors, status=400)
    #
    #     return Response(AssetTypeSerializer(asset_type).data, status=200)
    #
    # def update(self, request, pk=None):
    #
    #     try:
    #         asset_type = AssetType.objects.get(asset_type_id=pk)
    #         if asset_type.asset_type_status == DELETED:
    #             return Response({_('detail'): _('asset_type not found')}, status=400)
    #     except:
    #         return Response({_('detail'): _('asset_type not found')}, status=400)
    #
    #     asset_type_data = AssetTypeSerializer(asset_type, data=request.data, fields='asset_type_name')
    #
    #     if asset_type_data.is_valid():
    #         asset_type = asset_type_data.save()
    #     else:
    #         return Response(asset_type_data.errors, status=400)
    #
    #     return Response(AssetTypeSerializer(asset_type).data, status=200)

    def retrieve(self, request, pk=None):
        try:
            asset_type = AssetType.objects.get(asset_type_id=pk)
            if asset_type.asset_type_status == DELETED:
                return Response({_('detail'): _('asset_type not found')}, status=400)
        except:
            return Response({_('detail'): _('asset_type not found')}, status=400)

        return Response(AssetTypeSerializer(asset_type).data, status=200)

    # def destroy(self, request, pk=None):
    #     try:
    #         asset_type = AssetType.objects.get(asset_type_id=pk)
    #         if asset_type.asset_type_status == DELETED:
    #             return Response({_('detail'): _('asset_type not found')}, status=400)
    #     except:
    #         return Response({_('detail'): _('asset_type not found')}, status=400)
    #
    #     asset_type.asset_type_status = DELETED
    #     asset_type.save()
    #
    #     return Response({
    #         "asset_type_id": asset_type.asset_type_id,
    #         "status": "deleted"
    #     }, status=200)

    def list(self, request, *args, **kwargs):
        resort = get_resort_for_user(request.user)
        search = request.query_params.get('search', '')
        order_by = request.query_params.get('order_by', 'asset_type_name')
        order_by_direction = request.query_params.get('order_by_direction', 'desc')

        if order_by_direction == 'desc':
            order = '-' + order_by
        elif order_by_direction == 'asc':
            order = order_by

        query = AssetType.objects.filter(asset_type_name__icontains=search, resort=resort, asset_type_status=LIVE) \
            .order_by(order)
        queryset = self.filter_queryset(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AssetTypeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
