from decimal import Decimal


class ExportMixin:
    def write_file(
        self,
        sql: str,
        params: tuple,
        file_path: str,
        encoding: str,
        delimeter: str,
        quote: str,
    ):

        if quote.lower().startswith("0x"):
            quote = chr(int(quote, 16))
        if delimeter.lower().startswith("0x"):
            delimeter = chr(int(delimeter, 16))

        row_counter = 0
        with open(
            file_path,
            mode="w",
            encoding=encoding,
            errors="ignore",
        ) as writer:
            buf = []
            for row in self.read(sql, params):
                tmp_row = []
                for col in row:
                    if col is None:
                        tmp_row.append("")
                    elif isinstance(col, (int, float, Decimal, bool)):
                        tmp_row.append(f"{col}")
                    else:
                        tmp_row.append(f"{quote}{col}{quote}")
                line = delimeter.join(tmp_row)
                row_counter += 1
                buf.append(line.replace("\n", ""))
                if len(buf) >= 10000:
                    writer.write("\n".join(buf))
                    writer.write("\n")
                    buf.clear()
            if buf:
                writer.write("\n".join(buf))
                writer.write("\n")
        return row_counter

    def write_file_all_str(
        self,
        sql: str,
        params: tuple,
        file_path: str,
        encoding: str,
        delimeter: str,
        quote: str,
    ):

        if quote.lower().startswith("0x"):
            quote = chr(int(quote, 16))

        if delimeter.lower().startswith("0x"):
            delimeter = chr(int(delimeter, 16))

        x = f"{quote}{delimeter}{quote}"

        row_counter = 0
        with open(
            file_path,
            mode="w",
            encoding=encoding,
            errors="ignore",
        ) as writer:
            buf = []
            for row in self.read(sql, params):
                line = f"{quote}{x.join([str('' if col is None else col) for col in row])}{quote}"
                row_counter += 1
                buf.append(line.replace("\n", ""))
                if len(buf) >= 10000:
                    writer.write("\n".join(buf))
                    writer.write("\n")
                    buf.clear()
            if buf:
                writer.write("\n".join(buf))
                writer.write("\n")
        return row_counter

    def export(
        self,
        sql: str,
        params: tuple,
        file_path,
        encoding: str = "utf8",
        delimeter: str = ",",
        quote: str = '"',
        all_col_as_str: bool = True,
    ) -> int:
        """
        导出数据到文件到本地，返回导出的行数
        """

        if all_col_as_str:
            return self.write_file_all_str(
                sql, params, file_path, encoding, delimeter, quote
            )
        else:
            return self.write_file(sql, params, file_path, encoding, delimeter, quote)
