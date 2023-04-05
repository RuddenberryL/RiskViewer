import os
import xlrd
import tqdm

def csv_from_excel(dirs):
    try:
        xls_dir = dirs[0] + '/' + dirs[1]
        wb = xlrd.open_workbook(f'{xls_dir}.xls')
        sh = wb.sheet_by_name('所内合约行情报表')
        your_csv_file = open(f'./csv/{dirs[2]}/{dirs[1]}.csv', 'a')

        data = []
        start = 3
        end = sh.nrows-5
        und = ''
        for rownum in range(start, end):
            d = sh.row_values(rownum)
            if d[0] == '':
                d[0] = und
            else:
                und = d[0]
            data.append(','.join('%s'%i for i in d))
        for d in data:
            your_csv_file.write(d+'\n')

        your_csv_file.close()
    except Exception as e:
        print(f"Error: {dirs[0]}{dirs[1]} with exception: {e}")

def csv_from_text(dirs):
    txt_dir = dirs[0] + '/' + dirs[1]
    txt_file = open(f"{txt_dir}.txt", encoding='utf8')
    txts = txt_file.readlines()
    txts = txts[1:]
    csv_file = open(f'./csv/{dirs[2]}/{dirs[1]}.csv', 'a')
    for line in txts:
        d = line.replace(' ', '').split('|')
        line = ','.join(str(i.replace(',', '')) for i in d)
        csv_file.write(line)
    csv_file.close()
    txt_file.close()

def get_xls_files():
    xchanges = ['ine', 'shfe']
    file_paths = []
    for xchange in xchanges:
        for root, directories, files in os.walk(f'./data/{xchange}'):
            for filename in files:
                # filepath = os.path.join(root, filename)
                file_paths.append((root, filename[:-4], xchange))
    return file_paths

def get_txt_files():
    xchanges = ['czce']
    file_paths = []
    for xchange in xchanges:
        for root, directories, files  in os.walk(f'./data/{xchange}'):
            for filename in files:
                file_paths.append((root, filename[:-4], xchange))
    return file_paths

def run():

    txt_files = get_txt_files()

    file_paths = get_xls_files()

    paths = tqdm.tqdm(file_paths, ascii=True)

    for file in paths:
        csv_from_excel(file)

    paths = tqdm.tqdm(txt_files, ascii=True)
    for path in paths:
        csv_from_text(path)

if __name__ == '__main__':
    run()