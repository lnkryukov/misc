from flask import Flask, jsonify, request, abort, render_template, redirect
import bcrypt
import datetime
import uuid
import jwt

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAw/DLEeKLEwrz4leEhT/MeVBhxtc2uapN4E9ZATFzgLnoBJAv
FNFLti3l23ewqhMnf9FnYFhwHJnILBOgFXBwKPiOOL9nU/y2tQi9sratA4ZDHbhR
e95Hnt/T+Pjy8Hi+UzSCVygToUn5vzwRcACOj1TV+3OBYASGQ5l3MbHEwzXlqYwM
MTG3VciORA61u/R1N/RZ5uCNs5fWkRWrEI5GkiZ0MWK+jnJguiQCWSJozJBOrUNK
g811WT8lcuYN5mH1ERJvxlulEdg/x7iOYLGV24XSbLbKV3nInEXdUtJc6EdHM2U8
AsncC7bf5CipRZwuVSGpstRYHfyApnjyOor4BQIDAQABAoIBAEGdDsNsc1nrHwQ6
flwIozY0nqlxRBgkWXO13n4xyxXeKz3r8ngsJghZklFN4VDynRWGT/HJa7GIJans
4HyNbGGr6iRCpB1R0PUKekuwNHurqCn5oP+zzZP8LAWBiAjSxhkiykrZVsl59jH9
sXEqHpMMu6M6aKZ4nWVhrLJtbxBXE7rcCyIHI6mVvAMPU5ZmSQi7feoR1ufYd9mq
NVa/7x41fMR4+7cDiF72ATqnJMBZiv7Fl+fLFu8FAEKLB+QRlKZt905UYl325VAJ
MZYn2qa/EJn+TU6QkHUwy2YWRdY2WyeW/UBBE9mGALMbaJEulO6QMmvpT7ZRDIgV
p7W4xvkCgYEA77NW7KJH/fNq1ajDH2/2zcV1fL1v+CqqBysNnarSH8mcCuKUop7L
WwBMwPN0iYcq9Tc4E1puNGerK3kCEDfwO/fPccLa0xPz4qYx+mvkBIyq+FugKJYO
HlB0k7tfbSUMinwLpwkLrE5z9b1kW2JeUmQyRqWVv8WxGNlQz5JwRJcCgYEA0UOw
Zidq/88dPeGwh0aIeWHI/8PvEWXBLvTnVPxolcMw5/eB11iTgJloY51XF26pyLHg
3Rd3ZEmOYrutgqZI7w+SkuzyW/YVyP97OHyo+g180PSpdKYIXGB5KchUQi6Lj0Uf
5n/XAiU+sHd8wUVaq5yDl0NTmLL+IGv2PCPpL8MCgYEAv3+hpG+J4IMGCShIqucC
YCau1DdsKvG64PsuZ5Y/RRIGzlNyt/DxOgSlTUmzAuSwFzREYoHOpaNlBtgoI9js
3pv+aT5pIFVCdQKdzxk/E7tmJADflU08fk98s0Hw3PvKZyDvFkWNw9zxm5Pxh2ix
PlW6LOLBHnLMJ7QGca7mboUCgYB7u0grvpbXlkC1/CICekPrcVQFVnaelMm61/eI
Go5ELttV7NSK3capPQuqCrgaFMay8eoBEAT5+TwFSO741xU8tLp3wT4z/bc310em
SJ8o6pyoeGFRpXJAHJLHj7myQA8osTiBc4lPrXH5qUzMghNwcOSlpZtiKEN2LB+1
w433PQKBgQCmY6Ngvazq4iqzO1NfZmE1ZUJsuvmo8OYTq3JV3C2JHhIroRoblR9S
9/zVF90+mQSl+Qe7PzdbgaKYot4UE280duJ/mXtz/oxT8qt3mfnAFh1aEitsbywo
fOgHQgK39OGqydaRP5AlwGOWe4v/VndHfVKn4wEF5pCgHPr3QtbbDg==
-----END RSA PRIVATE KEY-----"""

users = [
    {   "name": "first",
        "password": b"abcd" },
    {   "name": "second",
        "password": b"1234" },
    {   "name": "third",
        "password": b"abcd1234" }
]

for i in users:
    i["password"] = bcrypt.hashpw(i["password"], bcrypt.gensalt())

app = Flask(__name__)

@app.route("/login", methods=["GET"])
def loginPage():
    redirectUri = request.args.get("redirectUri")
    return render_template("index.html", redirect=redirectUri)

@app.route("/getToken", methods=["GET"])
def token():
    username = request.args.get("username")
    password = request.args.get("password")
    redirectUri = request.args.get("redirectUri")

    db_user = list(filter(lambda u: u["name"] == username, users));
    
    if len(db_user) != 1:
        abort(404, "User not found")

    db_username = db_user[0]["name"]
    db_password = db_user[0]["password"]

    if not bcrypt.checkpw(password.encode('utf-8'), db_password):
        abort(403, "Wrong password")

    token = {
            "iss": "server2", # Кто выдал токен, тут должен быть url
            "sub": db_username, # Тут должен быть *уникальный* id юзера
            "aud": [
                "server1" # Кому предназначен токен, тут должен быть url
            ], 
            "exp": (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(), # Задаем время жизни токена, надо подобрать более кошерное (по RFC должен быть в POSIX)
            "iat": datetime.datetime.now().timestamp(), # Дата выдачи, тоже POSIX
            "jti": str(uuid.uuid4()) # Глобально уникальный id токена, для защиты от повторного использования. Нужно держать на принимающей стороне список отрботанных токенов
    }

    encoded = jwt.encode(token, private_key, algorithm="RS512")

    redirectUri = "http://{}?token={}".format(
        redirectUri,
        encoded.decode('utf-8')
    )

    return redirect(redirectUri, code=302)