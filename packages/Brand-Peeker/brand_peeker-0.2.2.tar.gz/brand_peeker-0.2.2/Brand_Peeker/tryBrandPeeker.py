import main
import getUrls

print("""\
██████╗ ██████╗  █████╗ ███╗   ██╗██████╗     ██████╗ ███████╗███████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██████╔╝███████║██╔██╗ ██║██║  ██║    ██████╔╝█████╗  █████╗  █████╔╝ █████╗  ██████╔╝
██╔══██╗██╔══██╗██╔══██║██║╚██╗██║██║  ██║    ██╔═══╝ ██╔══╝  ██╔══╝  ██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝    ██║     ███████╗███████╗██║  ██╗███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

1. Download favicon from url
2. Get the root url of a website
3. Get url from web browser query
4. Get icon from web browser query
5. Exit
""")

while True:
    selection = int(input('What do you want to do ? (Int): '))

    if selection == 1:
        print('Download favicon from url:')
        main.getIconByUrl(input('Type a valid url: '), input('path/to/filename.ico (press enter to skip): '))
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

    if selection == 2:
        print('Get the root url of a website:')
        print(getUrls.getRootUrl(input('Type a valid url: ')))
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

    if selection == 3:
        print('Get url from web browser query:')
        print(getUrls.getUrlByWebsearch(input('Type something: ')))
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

    if selection == 4:
        print('Get icon from web browser query:')
        main.getIconByName(input('Type something: '), input('path/to/filename.ico (press enter to skip): '))
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

    if selection == 5:
        print('...')
        break

