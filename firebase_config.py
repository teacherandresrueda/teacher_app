
def login_user(email, password):
    try:
        ref = db.collection("users").document(email)
        user = ref.get()

        if not user.exists:
            return False, "User not found"

        data = user.to_dict()

        if data["password"] == password:
            return True, "Login successful"
        else:
            return False, "Wrong password"

    except Exception as e:
        return False, str(e)
