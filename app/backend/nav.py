from flask_login import current_user

from app import nav


def create_nav():
    nav.Bar('main', [
        nav.Item('Übersicht', 'backend.dashboard', items=[nav.Item('Dashboard', 'backend.dashboard')]),
        nav.Item('Inhalte', 'backend.dashboard', items=[
            nav.Item("Seiten", 'backend.pages'),
            nav.Item("News", 'backend.news')
        ]),
    ])

    navbar_main = nav.bars.__getitem__('main')
    navbar_main_items = navbar_main.items

    # navigationpunkte für admins
    if current_user.is_admin:
        navbar_main_items.append(nav.Item('Backend Benutzer', 'backend.be_user', html_attrs={'class': ['home']}, items=[
            nav.Item('Übersicht', 'backend.be_user'),
            nav.Item('Benutzer hinzufügen', 'backend.add_be_user')
        ]))

    # navigationspunkte für admins und moderatoren
    if current_user.is_admin or current_user.is_moderator:
        navbar_main_items.append(nav.Item('System', 'backend.system', items=[
            nav.Item("Login Versuche", 'backend.failed_login_records'),
            nav.Item("System Mails", 'backend.system_mails'),
            nav.Item("Einstellungen", 'backend.system_settings'),
            nav.Item("Papierkorb", 'backend.trash')
        ]))

    # navigationspunkt account
    navbar_main_items.append(nav.Item('Account', '', items=[nav.Item("Account bearbeiten", 'backend.account_edit')]))
