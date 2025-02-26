import events from "../utils/Events.js";
import Message from "./Message.js";
import StatusMessage from "./StatusMessage.js";

const template = document.createElement('template');
template.innerHTML = `
    <style>
        :host {
            overflow: auto;
            flex-grow: 1;
            position: relative;
        }
        * {
            box-sizing: border-box;
        }
        .message-list-wrap {
            height: 100%;
        }
    </style>
    <div class="message-list-wrap">
        <div id="message_list"></div>
    </div>
`;


export default class MessageList extends HTMLElement {
    constructor() {
        super();
        this.message_list_element = null;
        this.on_assistant_response = this.on_assistant_response.bind(this);
        this.on_user_input = this.on_user_input.bind(this);
        this.conversation = [];
    }

    on_assistant_response(value) {
        // Append the response to the message list
        this.message_list_element.querySelector('k-status-message').remove();
        this.message_list_element.appendChild(new Message({is_user: false, html_content: value}));
        const list_elements = this.message_list_element.querySelectorAll('k-message');
        list_elements[list_elements.length-1].scrollIntoView();
    }

    on_user_input(user_input) {
        // Append user message to the message list
        this.message_list_element.appendChild(new Message({is_user: true, html_content: user_input}));

        // Add user message to conversation array
        this.conversation.push({role: "user", content: user_input, timestamp: new Date(Date.now()).toISOString()})
        
        // Show status message
        this.message_list_element.appendChild(new StatusMessage());
        const list_elements = this.message_list_element.querySelectorAll('k-message');
        list_elements[list_elements.length-1].scrollIntoView();
        
        // Get the response
        fetch('chat',
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({conversation: this.conversation})
        })
        .then(value => {
            return value.text()
        })
        .then(value => {
            this.conversation.push({role: "assistant", content: value, timestamp: new Date(Date.now()).toISOString()});
            events.on_event('assistant_response', value);
        });
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.message_list_element = template_element.getElementById('message_list');
            this.shadowRoot.appendChild(template_element);
        }
        events.register_callback('assistant_response', this.on_assistant_response);
        events.register_callback('user_input', this.on_user_input);
    }

    disconnectedCallback() { 
        events.unregister_callback('assistant_response', this.on_assistant_response);
        events.unregister_callback('user_input', this.on_user_input);
    }
}

window.customElements.define("k-message-list", MessageList);
