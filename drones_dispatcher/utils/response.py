
def generate_response(data=None, message=None, status=400):
    """
    Generates a dictionary response
    :param data: The data to send back to the client
    :param message: The message to display to the user
    :param status: The HTTP status code, defaults to BAD REQUEST
    :return: Dictionary with keys: data, message, status.
    """

    return {
        "data": data,
        "message": message,
        "status": status
    }
