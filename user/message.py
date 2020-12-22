def message(doamin, uid64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{doamin}/user/emailcheck/{uid64}/{token}\n\n감사합니다."

#domain- current site domain
#uid- urlsafe base64 encode force bytes (user.pk)
#token - account activation toekn make token(user)