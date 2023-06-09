from flask import Flask, render_template, request, redirect, url_for, jsonify
import hmac
import hashlib
import subprocess
import os

app = Flask(__name__)  # Standard Flask app


def verify_hmac_hash(data, signature):
    github_secret = bytes(os.environ['DISCORD_TOKEN'], 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)


@app.route("/payload", methods=['POST'])
def github_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct']:
                try:
                    gitdir = os.environ['GIT_DIR']
                    cmd_output = subprocess.check_output(['git', f'--git-dir={gitdir}', 'pull', 'origin', 'main'])
                    subprocess.check_output(['systemctl', 'restart', 'discord-bot.service'])
                    return jsonify({'msg': str(cmd_output)})
                except subprocess.CalledProcessError as error:
                    return jsonify({'msg': str(error.output)})
            else:
                return jsonify({'msg': 'nothing to commit'})

    else:
        return jsonify({'msg': 'invalid hash'})


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80)
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
