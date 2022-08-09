import argparse
from linker import _search, claim_mail, slug
from dotenv import load_dotenv


parser = argparse.ArgumentParser()
parser.add_argument(
    'cmd',
    help='(str) : Commande à executer',
    choices=('search', 'extract')

)
parser.add_argument(
    '--engines',
    '-e',
    help='(str[int]) : Moteurs de recherches à utiliser pour la recherche',
    default='01234'
)
parser.add_argument(
    '--search',
    '-S',
    help='(str) : Saisie de la recherche',
    default='Hello, world'
)
parser.add_argument(
    '--deep',
    '-d',
    help='(int) : Profondeur de la recherche',
    default=3,
    type=int
)
parser.add_argument(
    '--output',
    '-o',
    help='(str) : Nom du fichier de sortie des résultas de la recherche [les formats JSON et CSV sont supportés]',
    default=''
)

parser.add_argument(
    '--host',
    '-H',
    help='(str) : Lien du site d\'où les données doivent être extraites'
)

parser.add_argument(
    '--browser',
    '-b',
    choices=('chrome', 'firefox'),
    default='chrome',
    help='(str) : Web browser to use for crawling'
)

if __name__ == '__main__':
    load_dotenv()
    args = parser.parse_args()
    out = args.output if args.output else f'{slug(args.search)}:{args.engines}:{args.deep}.csv'.replace(
        '/', '-')
    if args.cmd == 'search':
        _search(
            browser=args.browser,
            engines=args.engines,
            search=args.search,
            out=out,
            deep=args.deep
        )
    elif args.cmd == 'extract':
        r = claim_mail(args.host)
        print('Host : {} \nEmail : {}\nTel : {}'.format(args.host, *r))
