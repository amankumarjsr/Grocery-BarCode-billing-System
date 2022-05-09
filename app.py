from logging import exception
from flask import Flask, render_template, request, Response
from camera import reader
from billing import calculator
from database import sql_database
from add_product import inserter


app = Flask(__name__)

device_id = []
selected_data = []
item_to_remove = []


@app.route("/contactus", methods=["GET"])
def Contact():
    return render_template("contactus.html")


@app.route("/team", methods=["GET"])
def team():
    return render_template("team.html")


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


# connecting to database and taking the product from temp db and removing the temp db file
@app.route("/remove_product", methods=["GET", "POST"])
def remove_product():
    try:
        sql_con = sql_database()
        # print(item_to_remove[-1])
        sql_con.data_remover(item_to_remove[-1][0])
        return render_template("add_product.html")
    except exception as exp:
        return render_template("add_product.html", error=exp)


# taking the product name and price and inserting that into productdb
@app.route("/added_product", methods=["GET", "POST"])
def added_product():
    try:
        product_name = request.form["product_name"]
        product_price = float(request.form["product_price"])
        sql_con = sql_database()  # connecting to db
        # print(item_to_remove[-1])
        sql_con.data_inserter(item_to_remove[-1][0], product_name, product_price)
        return render_template("add_product.html")
    except exception as exp:
        return render_template("add_product.html", error=exp)


# producing each frame of the video and transfering it to the html img tag
def gen_1(camera):
    while True:
        frame, data = camera.get_frame()
        if data not in selected_data:
            selected_data.append(data)
        yield (
            b"--frame\r\n" b"Content-Type:  image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


# producing each frame of the video and transfering it to the html img tag
def gen_2(add_product):
    while True:
        frame, data = add_product.add_product()
        if data not in item_to_remove:
            item_to_remove.append(data)
        # print(item_to_remove[-1])
        yield (
            b"--frame\r\n" b"Content-Type:  image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


# scanning barcode and checking for the barcode in the db or not
@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    try:
        try:
            device = request.form["device_id"]
            if device == "":
                device_id.append("0")
            else:
                device_id.append(device)
        except:
            device_id.append("0")
        return render_template("scanner.html")
    except exception as exp:
        return render_template("scanner.html", error=exp)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    try:
        try:
            device = request.form["device_id"]
            device_id.append(device)
            if device == "":
                device_id.append("0")
            else:
                device_id.append(device)
        except:
            device_id.append("0")
        return render_template("add_product.html")
    except exception as exp:
        return render_template("add_product.html", error=exp)


@app.route("/video", methods=["GET", "POST"])
def video():
    capture_device = device_id[-1]
    capture_device = int(capture_device)
    return Response(
        gen_1(reader(capture_device)),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/video_add_product", methods=["GET", "POST"])
def video_add_product():
    capture_device = device_id[-1]
    capture_device = int(capture_device)
    return Response(
        gen_2(inserter(capture_device)),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


# getting all the data and generating bill and html table which will be shown using jinja
@app.route("/results", methods=["GET", "POST"])
def results():
    try:
        sql_con = sql_database()
        whole_data = sql_con.get_data()
        biller = calculator()
        list_data, total_bill = biller.bill(selected_data[-1], whole_data)
        heading = ["S.no", "Item", "Price"]
        return render_template(
            "results.html", headings=heading, data=list_data, total_bills=total_bill
        )
    except exception as exp:
        return render_template("results.html", error=exp)


if __name__ == "__main__":
    app.run(debug=True)
