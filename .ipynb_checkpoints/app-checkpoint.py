{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "31419679-ae22-4354-ad86-9c17b7ec4d98",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "\n",
    "st.title(\"AI-Powered Data Analysis & Visualization Assistant\")\n",
    "st.write(\"Upload a dataset to begin\")\n",
    "\n",
    "file = st.file_uploader(\"Upload CSV file\", type=[\"csv\"])\n",
    "\n",
    "if file is not None:\n",
    "    df = pd.read_csv(file)\n",
    "    st.subheader(\"Dataset Preview\")\n",
    "    st.dataframe(df.head())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d5f93a62-7933-4fe1-bef3-9d9779aa6f12",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:python-cvcourse]",
   "language": "python",
   "name": "conda-env-python-cvcourse-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.14"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
