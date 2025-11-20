class Calculator {
    constructor(displayElement) {
        this.displayElement = displayElement;
        this.clear();
    }

    clear() {
        this.expression = '';
        this.isResultShown = false;
        this.updateDisplay();
    }

    delete() {
        if (this.isResultShown) {
            this.clear();
            return;
        }
        this.expression = this.expression.toString().slice(0, -1);
        this.updateDisplay();
    }

    append(value) {
        if (this.expression === 'Error') {
            this.expression = '';
        }
        if (this.isResultShown && !['+', '-', '*', '/'].includes(value)) {
            this.expression = '';
        }
        this.isResultShown = false;

        const lastChar = this.expression.slice(-1);
        const isValueOperator = ['+', '-', '*', '/'].includes(value);
        const isLastCharOperator = ['+', '-', '*', '/'].includes(lastChar);

        if (isValueOperator && isLastCharOperator) {
            this.expression = this.expression.slice(0, -1) + value;
        } else {
            this.expression += value;
        }
        
        this.updateDisplay();
    }

    compute() {
        const lastChar = this.expression.slice(-1);
        if (['+', '-', '*', '/'].includes(lastChar) || this.expression === '') {
            return;
        }

        try {
            const result = new Function('return ' + this.expression)();

            if (!isFinite(result)) {
                this.expression = 'Error';
            } else {
                this.expression = result.toString();
            }
            this.isResultShown = true;
        } catch (e) {
            this.expression = 'Error';
            this.isResultShown = true;
        }
        this.updateDisplay();
    }

    updateDisplay() {
        this.displayElement.innerText = this.expression || '0';
    }
}

const display = document.querySelector('.display');
const buttons = document.querySelectorAll('button');
const calculator = new Calculator(display);

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.innerText;
        switch (value) {
            case 'AC':
                calculator.clear();
                break;
            case 'DEL':
                calculator.delete();
                break;
            case '=':
                calculator.compute();
                break;
            default:
                calculator.append(value);
                break;
        }
    });
});