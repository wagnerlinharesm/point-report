import jwt


class JwtUtil:
    def __init__(self, jwt_token):
        self._decoded_token = jwt.decode(
            jwt_token,
            algorithms=['RS256'],
            options={"verify_signature": False}
        )

    def get_attribute(self, name):
        return self._decoded_token.get(name)
