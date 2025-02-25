import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: mandyc <filename>.md or mandy <filename>.md")
        sys.exit(1)

    if sys.argv[1] in ("--help", "-h"):
        print("Mandy Compiler Help:")
        print("Usage: mandyc <filename>.md")
        print("Commands:")
        print("  WRITE  - Print output")
        print("  TAKE   - Assign variables")
        print("  !!     - Comments")
        sys.exit(0)

    filename = sys.argv[1]
    
    try:
        with open(filename, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    from mandy_lang.lexer import Lexer
    from mandy_lang.parser import Parser
    from mandy_lang.vm import MandyVM

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    vm = MandyVM()
    vm.execute(ast)

if __name__ == "__main__":
    main()
