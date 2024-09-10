from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import SignUpSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserManageAPIView(APIView):
    def get_permissions(self):
        # 로그인 없이 회원가입 가능
        if self.request.method == "POST":
            return [AllowAny()]
        # 로그인 필수로 회원탈퇴 가능
        elif self.request.method == "DELETE":
            return [IsAuthenticated()]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # 계정 삭제 기능 (이 시점에서 인증된 사용자만 접근 가능)
        password = request.data.get("password")
        user = request.user

        # 비밀번호 확인
        if not user.check_password(password):
            return Response(
                {"detail": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자 계정 삭제
        user.delete()
        return Response(
            {"detail": "계정이 성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        if request.user.username != username:
            return Response(
                {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return Response(
                {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"detail": "기존 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {"detail": "새 비밀번호는 기존 비밀번호와 다르게 설정해야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "비밀번호가 성공적으로 변경되었습니다."},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 요청에서 refresh_token을 가져옴
            refresh_token = request.data["refresh_token"]
            # 토큰을 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()  # 이 메서드가 토큰을 블랙리스트로 만듦

            return Response({"detail": "로그아웃 성공"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": "토큰이 유효하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
