from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired,URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Location URL', validators=[URL()])
    cafe_opentime = SelectField('Cafe Opening Time', validators=[DataRequired()],choices=["8AM","9AM","10AM","11AM","12PM"])
    cafe_closetime = SelectField('Cafe Closing Time', validators=[DataRequired()],choices=["8PM","9PM","10PM","11PM","12AM"])
    cafe_coffeerating = SelectField('Cafe Coffee Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                    validators=[DataRequired()])
    cafe_wifirating = SelectField('Cafe Wifi Rating', choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                                  validators=[DataRequired()])
    cafe_powerrating = SelectField('Cafe Power Rating', choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                                   validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        to_be_added = [form.cafe_name.data, form.cafe_location.data, form.cafe_opentime.data, form.cafe_closetime.data,
                       form.cafe_coffeerating.data, form.cafe_wifirating.data, form.cafe_powerrating.data]
        print(to_be_added)
        with open('cafe-data.csv', "a" , newline='', encoding="utf8") as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(to_be_added)
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
