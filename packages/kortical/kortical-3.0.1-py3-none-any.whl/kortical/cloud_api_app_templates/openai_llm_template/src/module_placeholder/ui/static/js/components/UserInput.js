import events from "../utils/Events.js";

const template = document.createElement('template');
template.innerHTML = `
    <style>
        @import "./static/css/scrollbar.css";
        :host {
            display: flex;
            padding: 15px 0;
            margin-top: auto;
            align-self: stretch;
            border-radius: 26px;
            padding: 20px 0px 20px 24px;
            background: #282843;
            position: relative;
        }
        :host::before {
            content: '';
            position: absolute;
            left: 0;
            bottom: 100%;
            display: block;
            width: 100%;
            height: 25px;
            background: linear-gradient(#00000000, #1A1823);
        }
        * {
            box-sizing: border-box;
            font-family: var(--font-family);
            letter-spacing: .5px;
        }
        #user_input {
            background: #282843;
            border: none;
            outline: none;
            width: 100%;
            color: var(--white);
            font-size: 12px;
            line-height: 14px;
            max-height: 200px;
            resize: none;
            padding: 0 65px 0 0;
        }
        #submit {
            position: absolute;
            display: block;
            height: 20px;
            right: 25px;
            bottom: 16px;
            appearance: none;
            background: transparent;
            border: none;
            outline: none;
            padding: 0;
            cursor: pointer;
        }
        .disabled {
            pointer-events:none;
        }
    </style>
    <textarea type="text" id="user_input" name="user_input" placeholder="Enter your question here..." max-height="300" rows="1"></textarea>
    <button type="button" id="submit">
        <img src="./static/images/submit_arrow.svg">
    </button>
`;


export default class UserInput extends HTMLElement {
    constructor() {
        super();
        this.user_input_element = null;
        this.submit_element = null;
        this.on_submit = this.on_submit.bind(this);
        this.resize = this.resize.bind(this);
        this.disable_input = this.disable_input.bind(this);
        this.enable_input = this.enable_input.bind(this);
        this.keydown_event = this.keydown_event.bind(this);
    }

    disable_input() {
        this.submit_element.setAttribute('disabled', true);
        this.user_input_element.classList.add('disabled');
    }
    
    enable_input() {
        this.submit_element.removeAttribute('disabled');
        this.user_input_element.classList.remove('disabled');
    }

    on_submit() {
        if(this.user_input_element.value) {
            events.on_event('user_input', this.user_input_element.value);
            this.user_input_element.value = '';
            this.disable_input();
            this.resize();
        } else {
            return
        };
    }

    keydown_event(e){
        if (e.key == 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.submit_element.click();
        }
    }

    resize() {
        this.user_input_element.style.height = 'auto';
        this.user_input_element.style.height = `${Math.min(this.user_input_element.scrollHeight, this.user_input_element.getAttribute("max-height"))}px`;
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.user_input_element = template_element.getElementById('user_input');
            this.submit_element = template_element.getElementById('submit');
            this.shadowRoot.appendChild(template_element);
        }

        this.user_input_element.addEventListener('keydown', this.keydown_event);
        this.user_input_element.addEventListener('input', this.resize);
        this.submit_element.addEventListener('click', this.on_submit);

        events.register_callback('assistant_response', this.enable_input);
    }

    disconnectedCallback() {
        this.user_input_element.removeEventListener('input', this.resize);
        this.submit_element.removeEventListener('click', this.on_submit);
        this.user_input_element.removeEventListener('keydown', this.keydown_event);
        
        events.unregister_callback('assistant_response', this.enable_input);
    }
}

window.customElements.define("k-user-input", UserInput);
