class calculator:
    def bill(self, selected_product, whole_data):
        product_name = []
        product_price = []
        list_data = []
        Serial_no = 1
        for item in selected_product:
            product_name.append(whole_data[item][0])
            product_price.append(whole_data[item][1])

        for item1, item2 in zip(product_name, product_price):
            list_data.append([Serial_no, item1, item2])
            Serial_no += 1
        bill = sum(product_price)
        total_bill = ["", "Total Bill:", bill]
        return list_data, total_bill
