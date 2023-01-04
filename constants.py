OLX_URL = 'https://www.olx.ro/d/imobiliare/apartamente-garsoniere-de-vanzare/2-camere/iasi_39939/q-apartament/?currency=EUR&search%5Bprivate_business%5D=private&search%5Border%5D=created_at:desc'

BASE_OLX_URL = 'https://www.olx.ro'

CONNECTION_LINK = 'mongodb+srv://danicai:1234@cluster0.fkguf.mongodb.net/?retryWrites=true&w=majority'

# List of all main locations in Iasi County, Romania
IASI_LOCATIONS =[
    'Alexandru cel Bun',
    'Bucium',
    'Bucsinescu',
    'Bularga',
    'C.U.G.',
    'Canta',
    'Cantemir',
    'Centru',
    'Centrul Civic',
    'Copou',
    'Crucea Rosie',
    'Dacia',
    'Frumoasa',
    'Galata',
    'Gara',
    'Manta Rosie',
    'Mircea cel Batran',
    'Moara de Foc',
    'Moara de Vant',
    'Nicolina',
    'Oancea',
    'Pacurari',
    'Podu Ros',
    'Podul de Fier',
    'Poitiers',
    'Piata Unirii',
    'Royal town',
    'Rediu',
    'Sararie',
    'Socola',
    'Stefan cel mare',
    'Stejar',
    'Tatarasi',
    'Targu Cucu',
    'Tudor Vladimirescu',
    'Ticau',
    'Uzinei',
    'Valea lupului',
    'Visan',
    'Zimbru'
]

IASI_LOCATIONS = [location.lower() for location in IASI_LOCATIONS]

aliases = {
    'cug': 'c.u.g.',
    'ultracentral': 'centru',
}