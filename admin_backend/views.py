from django.http import Http404
from admin_backend.business.computer_hardware import cal_computer_spec_combination
from admin_backend.models import (
    Inventory,
    Parameter,
    Hardware,
    InventoryExtra,
    StandardProductAsin,
)
from rest_framework import permissions, viewsets, generics
from django.db.models import Sum, Max
from rest_framework.response import Response
from rest_framework.request import Request


from admin_backend.serializers import (
    InventoryGroupSerializer,
    InventorySerializer,
    ParameterSerializer,
    InventoryExtraSerializer,
    HardwareSerializer,
    StandardProductAsinSerilizer,
    MyTokenObtainPairSerializer,
)

from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {"code": 0, "message": "OK", "data": serializer.validated_data},
            status=status.HTTP_200_OK,
        )


class SwitchRoleView(APIView):
    def post(self, request, *args, **kwargs):
        user_and_token = JWTAuthentication().authenticate(request)
        role = request.data["role"]

        if user_and_token is None:
            return Http404  # better
        user = user_and_token[0]

        token = RefreshToken.for_user(user)
        # Add custom claims
        token["role"] = role

        data = {}
        data["refresh"] = str(token)
        data["access"] = str(token.access_token)

        update_last_login(None, user)
        print(data)
        return Response(
            {"code": 0, "message": "OK", "data": data},
            status=status.HTTP_200_OK,
        )


class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Inventory.objects.filter(supplier__exact="").order_by("upc_full", "-qty")
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["upc", "wh_id"]


class ParameterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Parameter.objects.all().order_by("name")
    serializer_class = ParameterSerializer
    permission_classes = [permissions.IsAuthenticated]


class StandardProductAsinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = StandardProductAsin.objects.all().order_by(
        "memory", "disk", "operatingSystem"
    )
    serializer_class = StandardProductAsinSerilizer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["upc"]


class HardwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    permission_classes = [permissions.IsAuthenticated]
    update_data_pk_field = "upc"

    ## create or update
    def create(self, request, *args, **kwargs):
        kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return super().create(request, *args, **kwargs)


class InventoryExtraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = InventoryExtra.objects.all()
    serializer_class = InventoryExtraSerializer
    permission_classes = [permissions.IsAuthenticated]
    update_data_pk_field = "upc"

    ## create or update
    def create(self, request, *args, **kwargs):
        kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return super().create(request, *args, **kwargs)


class InventoryGroupList(generics.ListAPIView):
    queryset = (
        Inventory.objects.filter(supplier__exact="")
        .values("upc")
        .annotate(total_qty=Sum("qty"), product=Max("product"))
        .order_by("-total_qty")
    )
    serializer_class = InventoryGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class StandardProductCreate(generics.CreateAPIView):
    def create(self, request: Request):
        upc = request.data["upc"]
        combination = self._computer_spec_combination(upc)
        for mem, disk, system in combination:
            sp_asin = StandardProductAsin.objects.filter(
                upc=upc,
                operatingSystem=system,
                memory=int(mem),
                disk=int(disk),
                asin="",
            ).first()
            if not sp_asin:
                StandardProductAsin(
                    upc=upc,
                    operatingSystem=system,
                    memory=mem,
                    disk=disk,
                    asin="",
                ).save()

        return Response(data=combination)

    def _computer_spec_combination(self, upc):
        hardware_of_upc = Hardware.objects.filter(upc=upc).first()
        parameters = {para.name: para.value for para in Parameter.objects.all()}
        diskSizeList = [i.strip() for i in parameters["diskSize"].split(",")]
        memSizeList = [i.strip() for i in parameters["memSize"].split(",")]
        os = hardware_of_upc.os_version
        combination = cal_computer_spec_combination(diskSizeList, memSizeList, os)
        return combination
