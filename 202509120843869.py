def generate_serial_numbers(self, item_data, submitter: str, quantity: int, prod_type: str):
    """生成序列号"""
    try:
        # 连接数据库
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)

        # 获取当前日期信息
        now = datetime.datetime.now()
        year = str(now.year)[-2:]  # 年份后两位
        week = f"{now.isocalendar()[1]:02d}"  # 周数，补零到两位

        # 准备基础信息
        category_code = item_data[2]  # 产品类别
        subcategory_code = item_data[3]  # 产品子类
        delivery_type_code = item_data[4]  # 交付物类型码
        product_type_code = item_data[5]  # 产品类型码
        delivery_state_code = item_data[6]  # 交付物状态码
        flow_number = item_data[7]

        # 生成序列号
        serial_numbers = []
        for _ in range(quantity):
            # 生成8位唯一标识
            unique_id = str(uuid.uuid4().int)[:8]

            # 组装序列号：M/S + 2位产品类别 + 3位产品子类 + 3位交付物(交付物类型、产品类型、交付物状态) + 4位流水号 + 2位年 + 2位周数 + 8位唯一标识
            delivery_info = f"{delivery_type_code}{product_type_code}{delivery_state_code}"
            serial_number = f"{prod_type}{category_code:02}{subcategory_code:03}{delivery_info}{flow_number:04}{year:02}{week:02}{unique_id}"

            # 保存到数据库
            cursor.execute("""
                            INSERT INTO serial_numbers
                                (serial_number, product_serial, submitter, prod_type, create_time)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (serial_number, item_data[1], submitter, prod_type, now))

            serial_numbers.append(serial_number)

        conn.commit()