def signing_form(request, set_query):
    if request.method == 'POST':
        # VARIABLES
        cui = request.POST['cui']
        nit = request.POST['nit']
        name = request.POST['name']
        birth = request.POST['birth'].replace('-', '/')
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # QUERIES
        if (str(password) == str(confirm_password)):
            set_query(
                f'INSERT INTO SingleUser VALUES ({cui}, {nit}, "{name}", "{birth}", "{username}", "{password}", {phone});')


def business_signing_form(request, set_query):
    if request.method == 'POST':
        # VARIABLES
        businessType = request.POST.get('businessType', 'Sociedad anónima')
        name = request.POST['name']
        comercialName = request.POST['comercialName']
        agent = request.POST['agent']
        agent = request.POST['agent']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # QUERIES
        if str(password) == str(confirm_password):
            set_query(
                f'INSERT INTO BusinessUser VALUES ("{comercialName}", "{businessType}", "{name}", "{agent}", "{password}", {phone});')
