from flask import Flask, redirect, render_template, request, url_for, session
from model import Model as mdl

newMdl = mdl
print(newMdl.check_tags("Music"))

pic = "60dcae4e5b00ffafd0e96d513a321-974509349.jpg"

photo = pic.replace("'", "")
foto = photo.replace("-","_")
picture = foto.replace(" ", "_")

print(picture)