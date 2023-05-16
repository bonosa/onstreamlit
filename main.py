"""
Module for currency exchange

This module provides several string parsing functions to implement a simple
currency exchange routine using an online currency service. The primary function
in this module is exchange().

Author: Saroj Bono
Date:   05/10/2023
"""
import os

# Use os.getenv() method which returns None if the environment variable is not present
APIKEY = os.getenv('keyA')

if APIKEY is None:
    raise Exception("Couldn't find 'keyA' in the environment variables!")

def before_space(s):
    """
    Returns the substring of s up to, but not including, the first space.
    
    Example: before_space('Hello World') returns 'Hello'
    
    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """
    # Check the preconditions
    assert isinstance(s, str)
    assert ' ' in s

    index_of_space = introcs.find_str(s, ' ')
    return s[:index_of_space]


def after_space(s):
    """
    Returns the substring of s after the first space

    Example: after_space('Hello World') returns 'World'

    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """
    # Check the preconditions
    assert isinstance(s, str)
    assert ' ' in s

    #introcs.assert_equals(True, type(s)==str and ' ' in s )
    index_of_space = introcs.find_str(s,' ')
    return s[index_of_space+1:]  


def first_inside_quotes(s):
    """
    Returns the first substring of s between two (double) quote characters

    Note that the double quotes must be part of the string.  So "Hello World" is a 
    precondition violation, since there are no double quotes inside the string.

    Example: first_inside_quotes('A "B C" D') returns 'B C'
    Example: first_inside_quotes('A "B C" D "E F" G') returns 'B C', because it only 
    picks the first such substring.

    Parameter s: a string to search
    Precondition: s is a string with at least two (double) quote characters inside
    """
    

    # enforce preconditions
    assert isinstance(s, str), "Input is not a string"
    assert introcs.count_str(s,'"') >= 2

    # find the first quote index
    first_quote_index = introcs.find_str(s, '"')

    # find the second quote index
    second_quote_index = introcs.find_str(s, '"', first_quote_index + 1)

    # return the substring between the two quote indices
    return s[first_quote_index + 1:second_quote_index]


def get_src(json):
    
    """
    Returns the src value in the response to a currency query.
        
    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"src"'. For example,
    if the json is
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns '2 United States Dollars' (not '"2 United States Dollars"'). 
    On the other hand if the json is 
        
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns the empty string.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """

    
    # enforce preconditions
    assert isinstance(json, str)
    #introcs.assert_true( isinstance(json, str))


    # find the index of '"src":'
    src_index = introcs.find_str(json, '"src":')

    

    # find the substring from the src_index onwards
    json_substring = json[src_index+6:]

    # get the first string inside quotes in the substring
    src_value = first_inside_quotes(json_substring)

    return src_value


def get_dst(json):
    """
    Returns the dst value in the response to a currency query.

    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"dst"'. For example,
    if the json is
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns '1.772814 Euros' (not '"1.772814 Euros"'). On the other
    hand if the json is 
    
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns the empty string.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
"""

    # enforce preconditions
    #introcs.assert_equals(True, isinstance(json, str))
    #introcs.assert_equals(True, isinstance(json, str))
    assert  isinstance(json, str)
    
    
    # find the '"dst"' substring in the json string
    dst_index = introcs.find_str(json, '"dst"')
    
    # return the substring after '"dst"'
    return first_inside_quotes(json[dst_index + 6:])


def has_error(json):
    """
    Returns True if the response to a currency query encountered an error.

    Given a JSON string provided by the web service, this function returns True if the
    query failed and there is an error message. For example, if the json is
        
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns True (It does NOT return the error message 
    'Source currency code is invalid'). On the other hand if the json is 
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns False.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """
    
    # enforce precondition
    assert isinstance(json, str)

    # find the index of the substring '"error"'
    error_index = introcs.find_str(json, '"error"')

    # find the quoted text following '"error"'
    error_message = first_inside_quotes(json[error_index+8:])

    # return True if error_message is not empty, and False otherwise
    return bool(error_message)
import introcs

def service_response(src,dst,amt):

    """
    Returns a JSON string that is a response to a currency query.

    A currency query converts amt money in currency src to the currency dst. The response 
    should be a string of the form

        '{"success": true, "src": "<src-amount>", dst: "<dst-amount>", error: ""}'

    where the values src-amount and dst-amount contain the value and name for the src 
    and dst currencies, respectively. If the query is invalid, both src-amount and 
    dst-amount will be empty, and the error message will not be empty.

    There may or may not be spaces after the colon.  To test this function, you should
    chose specific examples from your web browser.

    Parameter src: the currency on hand
    Precondition src is a nonempty string with only letters

    Parameter dst: the currency to convert to
    Precondition dst is a nonempty string with only letters

    Parameter amt: amount of currency to convert
    Precondition amt is a float or int
    """
    
    # Enforce preconditions
    assert isinstance(src, str), "src must be a string"
    assert isinstance(dst, str), "dst must be a string"
    assert isinstance(amt, (float, int)) and not isinstance(amt,bool)
    assert introcs.isalpha(src), "src must contain only letters"
    assert introcs.isalpha(dst), "dst must contain only letters"

    # Form the URL
    url = (
    f'https://ecpyfac.ecornell.com/python/currency/fixed?'
    f'src={src}&dst={dst}&amt={amt}&key={APIKEY}'
)

    # Make the request and read the response
    
    response=introcs.urlread(url)

    # Return the response
    return response


def iscurrency(currency):

    """
    Returns True if currency is a valid (3 letter code for a) currency.

    It returns False otherwise.

    Parameter currency: the currency code to verify
    Precondition: currency is a nonempty string with only letters
    """
    #result=isinstance(currency, str) and currency != '' and currency.isalpha()
    
    assert isinstance(currency, str), 'currency must be a string'
    assert currency != '', 'currency must not be empty'
    assert currency.isalpha(), 'currency must contain only letters'
    
    # Enforce preconditions
    #assert True,result
    
    # Use service_respon_se to check if currency conversion from the given currency to itself is successful
    response = service_response(currency, currency, 1)
    
    # Use has_error function to check if there was an error in the response
    error = has_error(response)
    
    # If there was an error, then the currency is not valid. Return not error to get the correct boolean result.
    return not error


def exchange(src,dst,amt):
    """
    Returns the amount of currency received in the given exchange.

    In this exchange, the user is changing amt money in currency src to the currency 
    dst. The value returned represents the amount in currency currency_to.

    The value returned has type float.

    Parameter src: the currency on hand
    Precondition src is a string for a valid currency code

    Parameter dst: the currency to convert to
    Precondition dst is a string for a valid currency code

    Parameter amt: amount of currency to convert
    Precondition amt is a float or int
    """

    
    # Enforce preconditions
    assert isinstance(src, str)
    assert isinstance(dst, str)
    assert isinstance(amt, (float, int))
    assert iscurrency(src)
    assert iscurrency(dst)

    # Get service response
    response = service_response(src, dst, amt)

    # Extract the destination amount from the response
    dst_amt_with_currency = get_dst(response)
    
    # Parse out the float value from the destination amount string
    # (Assuming the format is "<amount> <currency>")
    # Leveraging short-circuiting behavior in Python's boolean expressions
    dst_amt = has_error(response) and None or float(
        dst_amt_with_currency.split()[0])

    return dst_amt
import streamlit as st
#import currency  # Assuming currency.py holds your logic functions

import streamlit as st


def convert_currency(src: str, dst: str, amt: float) -> str:
    # Use your exchange function
    result = exchange(src, dst, amt)
    return f"You can exchange {amt} {src} for {result} {dst}."

# Create input fields in the Streamlit app
st.title('Currency Converter')
src = st.text_input('Enter the source currency code:')
dst = st.text_input('Enter the destination currency code:')
amt = st.number_input('Enter the amount in the source currency:', min_value=0.0)

if st.button('Convert'):
    result = convert_currency(src, dst, amt)
    st.write(result)
