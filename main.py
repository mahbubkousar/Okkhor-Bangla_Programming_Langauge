from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.ast_visualizer import ASTVisualizer


def main():
    # Example usage
    source_code = '''
    মূলকাজ main() {
        সংখ্যা x = 10;
        যদি (x > 5) {
            ফেরত x;
        }
    }
    '''

    try:
        # Lexical analysis
        print("Starting lexical analysis...")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print("\nTokens generated:")
        for token in tokens:
            print(token)

        # Parsing
        print("\nStarting parsing...")
        parser = Parser(tokens)
        ast = parser.parse()

        # Visualizing the AST
        print("\nAbstract Syntax Tree:")
        visualizer = ASTVisualizer()
        print(visualizer.visit(ast))

        print("\nParsing successful!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
