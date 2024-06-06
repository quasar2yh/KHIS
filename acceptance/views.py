from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from .serializers import ChargeItemSerializer, ClaimSerializer
from .models import ChargeItem, Claim
from account.models import Patient


class ChargeItemDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 테스트용 AllowAny
    def get(self, request, charge_item_id):
        charge_item = get_object_or_404(
            ChargeItem, pk=charge_item_id)
        serializer = ChargeItemSerializer(instance=charge_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, charge_item_id):
        charge_item = get_object_or_404(
            ChargeItem, pk=charge_item_id)
        serializer = ChargeItemSerializer(instance=charge_item, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChargeItemCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 테스트용 AllowAny

    def post(self, request):
        serializer = ChargeItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClaimListAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 테스트용 AllowAny

    def get(self, request):
        """
        Logic to check patients’ payment list at the hospital under various conditions
        """
        query_set = Claim.objects.all().order_by('-id')
        paginator = PageNumberPagination()

        # Extract query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status_filter = request.query_params.get('status')

        # Apply date range filtering
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            query_set = query_set.filter(
                created__date__range=[start_date, end_date])

        # Apply status filtering
        if status_filter:
            query_set = query_set.filter(status=status_filter)

        # Pagination & Serialize the filtered queryset
        result_page = paginator.paginate_queryset(query_set, request)
        claim_serializer = ClaimSerializer(result_page, many=True)
        return paginator.get_paginated_response(claim_serializer.data)


class PatientClaimCreateListAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 테스트용 AllowAny

    def post(self, request):
        """
        Logic to create a new patient claim
        """
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Logic to get patient claims
        """
        query_set = Claim.objects.all().order_by("-id")
        paginator = PageNumberPagination()

        # Extract query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status_filter = request.query_params.get('status')

        # Apply date range filtering
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            query_set = query_set.filter(
                created__date__range=[start_date, end_date])

        # Apply status filtering
        if status_filter:
            query_set = query_set.filter(status=status_filter)

        # Pagination & Serialize the filtered queryset
        result_page = paginator.paginate_queryset(query_set, request)
        claim_serializer = ClaimSerializer(result_page, many=True)
        return paginator.get_paginated_response(claim_serializer.data)


class PatientClaimDetailAPIView(APIView):
    """
    Logic to get, update, delete the patient claim
    """
    permission_classes = [permissions.AllowAny]  # 테스트용 AllowAny

    def get(self, request, claim_id):
        query_set = get_object_or_404(Claim, pk=claim_id)
        serializer = ClaimSerializer(query_set)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, claim_id):
        query_set = get_object_or_404(Claim, pk=claim_id)
        serializer = ClaimSerializer(query_set, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, claim_id):
        query_set = get_object_or_404(Claim, pk=claim_id)
        query_set.delete()
        return Response({"message":"successfully deleted."}, status=status.HTTP_200_OK)