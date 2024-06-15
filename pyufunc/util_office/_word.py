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
from pyufunc.util_pathio._platform import is_windows


def doc2pdf(doc_fname: str, pdf_fname: str = None, verbose: bool = False) -> None:
    """Convert a word document to pdf file on Windows platform

    Args:
        doc_fname (str): word document file name
        pdf_fname (str, optional): output pdf file name. Defaults to None.
        verbose (bool, optional): whether to print out message. Defaults to False.

    Raises:
        OSError: This function only works on Windows platform

    Returns:
        _type_: None

    Example:
        >>> from pyufunc import doc2pdf
        >>> doc2pdf('test.docx', 'test.pdf', verbose=True)
        Successfully convert test.docx to test.pdf
    """

    # check platform
    if not is_windows():
        print("This function only works on Windows platform")
        return None

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
