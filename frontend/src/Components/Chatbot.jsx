import { useState, useEffect, useRef } from "react";
import axios from "axios";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { AiOutlineClose, AiOutlineMessage } from "react-icons/ai";

dayjs.extend(relativeTime);

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [isSending, setIsSending] = useState(false);
    const [isChatOpen, setIsChatOpen] = useState(false);
    const chatDisplayRef = useRef(null);
    const textareaRef = useRef(null);

    const sendMessage = async () => {
        if (!input.trim() || isSending) return;

        setIsSending(true);
        const userMessage = { sender: "user", text: input, timestamp: new Date() };
        setMessages((prevMessages) => [...prevMessages, userMessage]);

        try {
            const response = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/chatbot`,
                { message: input }
            );
            const botMessage = { sender: "bot", text: response.data.response, timestamp: new Date() };
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
            console.error("Error communicating with the chatbot", error);
            const errorMessage = {
                sender: "bot",
                text: "Sorry, something went wrong. Please try again later.",
                timestamp: new Date(),
            };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        } finally {
            setIsSending(false);
            setInput("");
            adjustTextareaHeight();
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    useEffect(() => {
        if (chatDisplayRef.current) {
            chatDisplayRef.current.scrollTop = chatDisplayRef.current.scrollHeight;
        }
    }, [messages]);

    const adjustTextareaHeight = () => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
        adjustTextareaHeight();
    };

    // Toggle the chat interface
    const toggleChat = () => {
        setIsChatOpen(!isChatOpen);
    };

    return (
        <div className="relative">
            {!isChatOpen ? (
                // Chat Button View
                <button
                    onClick={toggleChat}
                    className="w-14 h-14 bg-pink-500 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-pink-600"
                >
                    <AiOutlineMessage className="text-2xl" />
                </button>
            ) : (
                // Chat Interface View
                <div className="flex flex-col w-[400px] p-4 bg-gray-100 rounded-lg shadow-lg h-[500px]">
                    <div className="flex justify-between items-center mb-2">
                        <h2 className="text-lg font-semibold">Chat with us</h2>
                        <button onClick={toggleChat} className="text-gray-500 hover:text-gray-700">
                            <AiOutlineClose className="text-2xl" />
                        </button>
                    </div>
                    <div
                        ref={chatDisplayRef}
                        className="flex-grow overflow-y-auto mb-4 p-2 bg-white rounded-lg"
                    >
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`p-2 my-1 rounded-md max-w-[80%] break-words relative ${
                                    msg.sender === "user"
                                        ? "bg-pink-100 ml-auto text-right"
                                        : "bg-gray-200 mr-auto text-left"
                                }`}
                            >
                                <p className="p-1">{msg.text}</p>
                                <span className="block text-xs text-gray-500 mt-1">
                                    {dayjs(msg.timestamp).fromNow()}
                                </span>
                            </div>
                        ))}
                    </div>
                    <div className="flex">
                        <textarea
                            ref={textareaRef}
                            value={input}
                            onChange={handleInputChange}
                            onKeyDown={handleKeyDown}
                            placeholder="Type your message..."
                            rows="1"
                            className="flex-grow p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-pink-500 resize-none"
                        />
                        <button
                            onClick={sendMessage}
                            className="bg-pink-500 text-white px-4 rounded-r-md hover:bg-pink-600 disabled:bg-pink-300"
                            disabled={isSending}
                        >
                            {isSending ? "Sending..." : "Send"}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
