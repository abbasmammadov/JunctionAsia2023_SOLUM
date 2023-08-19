from flask import Flask, render_template, request
from retail.owner.store_family_info import get_graph_parameters

app = Flask(__name__)

@app.route('/esl1')
def customer_website_1():
    return render_template('customer_website_1.html')

@app.route('/esl2')
def customer_website_2():
    return render_template('customer_website_2.html')

@app.route('/esl3')
def customer_website_3():
    return render_template('customer_website_3.html')


@app.route('/owner')
def customer_webpage():

    store = request.args.get('store')
    family = request.args.get('family')

    print(store, family)
    if store is None:
        store = 6
    if family is None:
        family = 'POULTRY'

    sales_data, lw, diss, up, new_prediction = get_graph_parameters(
        store, family)

    return render_template('owner.html', sales_data=sales_data, lw=lw, diss=diss, up=up, new_prediction=new_prediction)


@app.route('/owner', methods=["POST"])
def result():
    output = request.form.to_dict("owner.html")
    store = output['store']
    family = output['family']
    print(output)
    sales_data, lw, diss, up, new_prediction = get_graph_parameters(
        store, family)
    return render_template('owner.html', sales_data=sales_data, lw=lw, diss=diss, up=up, new_prediction=new_prediction)


if __name__ == '__main__':
    app.run(host='10.200.15.40', port=5000, debug=True)
