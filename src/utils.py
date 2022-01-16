import jwt


def get_user_login(request):
    token = request.headers.get('Authorization', None)
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(
        token, options={"verify_signature": False}
    )
    login = decoded_token.get('sub', None)
    return login
