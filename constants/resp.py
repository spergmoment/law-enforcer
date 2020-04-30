botlower = "I am at a lower level on the role hierarchy than this member."
userlower = 'This member has a higher role than you.'

owneronly = "You must be a bot owner to use this command."

def userperms(perm):
    return f"You must have the `{perm.upper()}` permission to do this."

def botperms(perm):
    return f"I lack the permissions to {perm}."