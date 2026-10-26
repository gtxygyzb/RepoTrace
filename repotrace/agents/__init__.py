"""Agent adapters. Each subclass only wraps run(): build the RepoTrace
message for this round, append it to the instruction, delegate to the vanilla
agent. Everything else (install, session, parsing, metrics) is untouched.
"""
