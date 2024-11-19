from rest_framework_simplejwt.authentication import JWTAuthentication

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from the cookies
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None

        try:
            # Validate the token
            validated_token = self.get_validated_token(access_token)

            # Get the user from the validated token
            user = self.get_user(validated_token)

            return (user, validated_token)
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Authentication error: {e}")
            return None