import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, session, redirect, url_for, send_from_directory, jsonify, request
from signin import checkPassword
from PYFiles.adminFunctions.NewProduct import multipleNewProduct
from PYFiles.adminFunctions.NewCompany import addCompanyToCompanyDatabase