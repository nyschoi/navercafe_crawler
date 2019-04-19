# # -*- coding: utf-8 -*-
# import configparser
# import json
# from flask import Flask, render_template, redirect, url_for, request, jsonify
# from cafe_kakao.kakaohandler import getAccessToken, getUserInfo
# app = Flask(__name__)

from cafe_kakao import app
if __name__ == '__main__':
    app.run(debug=True)