import csv
import os

from win32com import client
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook
from xlwt import easyxf

reports = [x for x in os.listdir('.\\src\\reports') if x.endswith('.csv')]
excel_file = 'UsageReport.xls'


def main():
    cwd = os.getcwd() + '\\'

    workbook = Workbook()
    with open(cwd + '\\src\\MonthlySummary.csv', 'r') as in_file:
        reader = csv.reader(in_file)
        worksheet = workbook.add_sheet('MonthlySummary')
        for r, row in enumerate(reader):
            for c, val in enumerate(row):
                worksheet.write(r, c, val)

    for report in reports:
        with open(cwd + '\\src\\reports\\' + report, 'r') as in_file:
            reader = csv.reader(in_file)
            worksheet = workbook.add_sheet(report[:-4])
            for r, row in enumerate(reader):
                for c, val in enumerate(row):
                    worksheet.write(r, c, val)

    # save and close file
    workbook.save(excel_file)

    # format for reports
    all_xf = easyxf('borders: left thin, right thin, top thin, bottom thin;'
                    'pattern: pattern solid, fore_color pale_blue;'
                    'font: bold False;'
                    'alignment: wrap True')

    header_xf = easyxf('borders: left thin, right thin, top thin, bottom thin;'
                       'pattern: pattern solid, fore_color light_blue;'
                       'font: color white, bold True;'
                       'alignment: wrap True')

    country_xf = easyxf('borders: left thin, right thin, top thin, bottom thin;'
                        'pattern: pattern solid, fore_color rose;'
                        'font: bold True;'
                        'alignment: wrap True')

    # format worksheet
    rb = open_workbook(excel_file)
    wb = copy(rb)
    for n, rs in enumerate(rb.sheets()):
        ws = wb.get_sheet(n)
        # formatting for all sheets
        for r in range(rs.nrows):
            for c in range(rs.ncols):
                ws.write(r, c, rs.cell(r, c).value, all_xf)
                # header
                if r == 0:
                    ws.write(r, c, rs.cell(r, c).value, header_xf)

        # sheet specific formatting
        if 'MonthlySummary' in ws.name:
            scalar = .7
            ws.col(0).width = int(scalar*7500)      # site
            ws.col(1).width = int(scalar*4500)      # first login
            ws.col(2).width = int(scalar*4500)      # last active
            for c in range(rs.ncols - 4, rs.ncols):
                ws.col(c).width = int(scalar*4500)      # events

            # quickly find country markers
            us_row, non_us_row, total_row = (0, 0, 0)
            for r in range(rs.nrows):
                v = rs.cell(r, 0).value
                if v == 'US.':
                    us_row = r
                elif v == 'Non-US':
                    non_us_row = r
                elif v == 'Total US and Non-US':
                    total_row = r

            for c in range(rs.ncols):
                ws.write(us_row, c, rs.cell(us_row, c).value, country_xf)
                ws.write(non_us_row, c, rs.cell(non_us_row, c).value, country_xf)
                ws.write(total_row, c, rs.cell(total_row, c).value, country_xf)
        else:
            scalar = .7
            ws.col(0).width = int(scalar * 4500)  # date
            ws.col(1).width = int(scalar * 7500)  # site
            for c in range(rs.ncols - 4, rs.ncols):
                ws.col(c).width = int(scalar * 4000)  # events

    wb.save(excel_file)

    # write out to pdf
    xl_app = client.Dispatch("Excel.Application")
    temp_book = xl_app.Workbooks.Open(cwd + excel_file)
    temp_book.WorkSheets.Select()
    temp_book.ActiveSheet.ExportAsFixedFormat(0, cwd + excel_file[:-4] + '.pdf')
    temp_book.Close(True)

    os.remove(excel_file)


if __name__ == '__main__':
    main()
