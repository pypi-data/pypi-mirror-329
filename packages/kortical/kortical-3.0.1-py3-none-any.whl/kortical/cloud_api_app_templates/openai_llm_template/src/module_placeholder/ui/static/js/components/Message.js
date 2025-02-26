
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
            background: linear-gradient(#0045AD, #007CD7);
            border-radius: 0 8px 8px 8px;
        }
        .user .message-status {
            text-align: right;
        }
        .user .message-content {
            margin-left: auto;
            background: linear-gradient(#FF00E5, #7D0088);
            border-radius: 8px 8px 0px 8px;
        }
    </style>
    <div class="message" id="message">
        <p class="message-status" id="message_status"></p>
        <p class="message-content" id="message_content"></p>
    </div>
`;


export default class Message extends HTMLElement {
    constructor(data) {
        super();
        this.message_element = null;
        this.message_content_element = null;
        this.timestamp = Date.now();
        this.is_user = data.is_user;
        this.html_content = data.html_content;
        this.get_time = this.get_time.bind(this);
    }

    get_time() {
        const dateObj = new Date(this.timestamp);
        const hours = dateObj.getHours() < 10 ? `0${dateObj.getHours()}` : dateObj.getHours();
        const minutes = dateObj.getMinutes() < 10 ? `0${dateObj.getMinutes()}` : dateObj.getMinutes();
        return `${hours}:${minutes}`;
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.message_element = template_element.getElementById('message');
            this.status_element = template_element.getElementById('message_status');
            this.message_content_element = template_element.getElementById('message_content');
            
            if(this.is_user) {
                this.status_element.innerText = `User - ${this.get_time()}`;
                this.message_element.classList.add('user');
            } else {
                this.status_element.innerText = `Kortical Chat - ${this.get_time()}`;
            }

            this.message_content_element.innerHTML = this.html_content;
            this.shadowRoot.appendChild(template_element);
        }
    }
}

window.customElements.define("k-message", Message);