# This data is used in the main script for searching the specified product and download it.

PROD_LIST_LINK = "https://vmssoftware.com/products/list/?license=Open%20Source"
PROD_LIST_REQ = r"/products/\w*-?\w*-?\w*"

PROD_LINK = "https://vmssoftware.com/products/"
PROD_START = "Latest Version"
PROD_END = "Download"
PROD_EXE_CSS = ".container-y-4 a:last-of-type"
PROD_REGEXP = r"https://vmssoftware.com/openkits/i64opensource/VSI-I64.{1,}ZIPEXE"
