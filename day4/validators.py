import string


def validate_yr(x):
    return len(x) == 4 and x.isnumeric()


def validate_byr(x):
    return validate_yr(x) and 1920 <= int(x) <= 2002


def validate_iyr(x):
    return validate_yr(x) and 2010 <= int(x) <= 2020


def validate_eyr(x):
    return validate_yr(x) and 2020 <= int(x) <= 2030


def validate_hgt(x):
    # Assumes that the unit is either "in" or "cm" (and thus two chars)
    x = x.strip()
    if not (x.endswith('in') or x.endswith('cm')):
        return False
    unit = x[-2:]
    val = int(x[:-2])
    if unit == 'cm':
        return 150 <= val <= 193
    if unit == 'in':
        return 59 <= val <= 76
    raise ValueError(f"Invalid height format: {x}")


def validate_hcl(x):
    if x[0] != '#':
        return False
    if len(x) != 7:
        return False
    valid_chars = string.ascii_lowercase[:6] + string.digits
    return all(y in valid_chars for y in x[1:])


def validate_ecl(x):
    valid_values = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    return x.strip() in valid_values


def validate_pid(x):
    return len(x) == 9 and x.isnumeric()


def validate_cid(x):
    return True


validators = {
    'byr': validate_byr,
    "iyr": validate_iyr,
    "eyr": validate_eyr,
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
    "cid": validate_cid,
}
