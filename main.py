import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from peewee import DoesNotExist

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET'])
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/new-donation/', methods=['GET', 'POST'])
def new_donation():
    if request.method == 'POST':
        donor_name = request.form.get('donor_name')
        donor = Donor.select().where(Donor.name == donor_name).get()
        try:
            donation_value = float(request.form.get('donation_value'))
        except ValueError:
            return render_template('newdonation.jinja2', error = "Please enter a number for donation value.")
        if donor is None:
            donor = Donor(name=donor_name).save()
        Donation(donor=donor, value=donation_value).save()
        return redirect(url_for('all'))
    else:
        return render_template('newdonation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

