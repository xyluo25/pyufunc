# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


# word to pdf
# word to text

from win32com.client import Dispatch
from pathlib import Path


def doc2pdf(doc_fname: str, pdf_fname: str = None, verbose: bool = False) -> None:

    # prepare input and out file names
    doc_fname = Path(doc_fname).resolve()
    if pdf_fname is None:
        pdf_fname = doc_fname.with_suffix('.pdf')
    else:
        pdf_fname = Path(pdf_fname).resolve()

    word = Dispatch('Word.Application')
    doc = word.Documents.Open(doc_fname)
    doc.SaveAs(pdf_fname, FileFormat=17)
    doc.Close()
    word.Quit()

    if verbose:
        print(f"Successfully convert {doc_fname} to {pdf_fname}")

    return None
