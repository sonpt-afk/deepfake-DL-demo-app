import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory

