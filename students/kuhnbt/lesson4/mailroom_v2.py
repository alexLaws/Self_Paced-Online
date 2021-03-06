#!/usr/bin/env python3
import os
import datetime

donor_info = {
             'Ernest Hemingway': [35, 65.25, 40],
             'John Steinbeck': [25.50, 20, 10],
             'Joseph Heller': [45, 20, 105.50],
             'Kurt Vonnegut': [60, 40, 400],
             'Michael Chabon': [100, 200, 300, 400]
             }


def start_program():
    """Prompt user for desired donor action and fulfill the request"""
    exit_program = False
    selection_dict = {'1': send_thankyou, '2': create_report,
                      '3': send_to_everyone, '4': quit_program}
    while not exit_program:
        selection = input('''Please enter a selection (1-4):
                           1. Send a thank you
                           2. Create a report
                           3. Send letters to everyone
                           4. Quit
                           ''')
        if selection_dict.get(selection, False):
            exit_program = selection_dict[selection]()
        else:
            print('Selection not found. Please enter a number 1-4')


def quit_program():
    return True


def send_thankyou():
    """Send a thank you note to person designated by user; add person to
       donor_info if they aren't already there"""
    while True:
        name = input('Please enter full name:\n')
        if name == 'list':
            print('This is the list of donor names:\n')
            for item in donor_info:
                print(item)
        else:
            donation = float(input('Please enter donation amount:\n'))
            if name in donor_info:
                donor_info[name].append(donation)
            else:
                donor_info[name] = [donation]
            print(get_thank_you(name))
            break
    return


def create_report():
    """Print summary report of donor info"""
    max_donor_width = 0
    for name in donor_info:
        if len(name) > max_donor_width:
            max_donor_width = len(name)
    print('{:{}}|{:12}|{:10}|{:8}'.format('Donor Name', max_donor_width,
          'Total Given', 'Num Gifts', 'Average Gift'))
    donor_list = list(donor_info.items())
    for donor in sorted(donor_list, key=lambda x: sum(x[1])):
        print('{:{}}|${:^11.2f}|{:^10}|${:^8.2f}'.format(donor[0],
              max_donor_width, sum(donor[1]), len(donor[1]),
              sum(donor[1])/len(donor[1])))


def send_to_everyone(directory=os.getcwd()):
    """Write thank you notes to specified directory for each donor in
       donor_info"""
    user_dir = input('Change output directory (y/n)?')
    if user_dir.lower() == 'y':
        directory = input('Please enter desired directory:')
    today = str(datetime.datetime.today())[:10]
    for donor in donor_info:
        filename = '/'.join([directory, donor])+'_' + today + '.txt'
        with open(filename, 'w') as f:
            print('Writing to ' + filename + '...')
            f.write(get_thank_you(donor))
        print('Finished!')


def get_thank_you(donor):
    """Return text of thank you letter for given donor"""
    donor_dict = {'name': donor, 'donation': donor_info[donor][-1],
                  'num_donations': len(donor_info[donor])}
    donor_dict['multiple'] = 's' if donor_dict['num_donations'] > 1 else ''
    thankyou = '''
    Dear {name}:
    Thank you for your generous donation of ${donation:.2f}.
    I really appreciate your {num_donations}
    donation{multiple} to our organization.
    I assure you that your contributions will be put to
    good use!
    Regards,
    Ben'''.format(**donor_dict)

    return thankyou


if __name__ == '__main__':
    start_program()
