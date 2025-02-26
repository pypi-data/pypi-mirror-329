
const template = document.createElement('template');
template.innerHTML = `
    <style>
        :host {
            display: block;
            padding: 15px 0;
        }
        * {
            box-sizing: border-box;
            font-family: var(--font-family);
            letter-spacing: .5px;
        }
        .message-status {
            font-size: 12px;
            line-height: 14px;
            color: var(--gray-light);
            margin: 0 0 10px 0;
        }
        .message-content {
            font-size: 12px;
            line-height: 14px;
            font-weight: 500;
            padding: 14px;
            width: fit-content;
            background: transparent;
            border-radius: 0 8px 8px 8px;
        }
    </style>
    <div class="message" id="message">
        <p class="message-status" id="message_status">Kortical is thinking</p>
        <p class="message-content" id="message_content"></p>
    </div>
`;


export default class StatusMessage extends HTMLElement {
    constructor() {
        super();
        this.message_element = null;
    }
    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.message_element = template_element.getElementById('message');
            this.shadowRoot.appendChild(template_element);
        }
    }
}

window.customElements.define("k-status-message", StatusMessage);