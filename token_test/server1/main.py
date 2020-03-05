from flask import Flask, request, render_template
import json
import bcrypt
import jwt

server2_public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw/DLEeKLEwrz4leEhT/M
eVBhxtc2uapN4E9ZATFzgLnoBJAvFNFLti3l23ewqhMnf9FnYFhwHJnILBOgFXBw
KPiOOL9nU/y2tQi9sratA4ZDHbhRe95Hnt/T+Pjy8Hi+UzSCVygToUn5vzwRcACO
j1TV+3OBYASGQ5l3MbHEwzXlqYwMMTG3VciORA61u/R1N/RZ5uCNs5fWkRWrEI5G
kiZ0MWK+jnJguiQCWSJozJBOrUNKg811WT8lcuYN5mH1ERJvxlulEdg/x7iOYLGV
24XSbLbKV3nInEXdUtJc6EdHM2U8AsncC7bf5CipRZwuVSGpstRYHfyApnjyOor4
BQIDAQAB
-----END PUBLIC KEY-----"""

app = Flask(__name__)

@app.route('/', methods=["GET"])
def main():
    return render_template("index.html")

@app.route('/loginWithToken', methods=["GET"])
def loginWithToken():
    token = request.args.get("token")
    decoded = jwt.decode(token, server2_public_key, issuer="server2", audience="server1")
    return render_template("login.html", user=decoded["sub"], token=decoded)