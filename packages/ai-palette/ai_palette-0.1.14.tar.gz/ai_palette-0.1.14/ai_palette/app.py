import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
from ai_palette import AIChat, Message
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), filename)

@app.route('/api/models', methods=['GET'])
def get_models():
    model_provider = request.args.get('type')
    api_key = request.args.get('api_key')
    
    try:
        models = AIChat.get_available_models(model_provider, api_key)
        if not models:
            return jsonify({'success': False, 'error': '不支持的模型类型或获取模型列表失败'}), 400
            
        return jsonify({'success': True, 'models': models})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        data = request.args
    else:
        data = request.json
        
    model_type = data.get('model_type')
    api_key = data.get('api_key')
    prompt = data.get('prompt')
    model = data.get('model')
    enable_streaming = data.get('enable_streaming', False)
    timeout = data.get('timeout', 120)  # 添加超时参数，默认120秒
    include_reasoning = data.get('include_reasoning', True)  # 是否包含思考过程
    context = data.get('context', [])  # 获取上下文
    
    try:
        # 根据不同的模型类型设置不同的参数
        chat_params = {
            'provider': model_type,  # 使用 model_type 作为 provider
            'api_key': api_key,
            'model': model,
            'enable_streaming': enable_streaming,
            'timeout': timeout
        }
        
        chat = AIChat(**chat_params)
        
        # 添加上下文消息
        for msg in context:
            # 如果是assistant的消息,需要过滤掉思考过程
            if msg['role'] == 'assistant':
                content = msg['content']
                # 如果内容包含<think>标记,只保留非思考部分
                if '<think>' in content:
                    # 移除<think>到</think>之间的内容
                    start = content.find('<think>')
                    end = content.find('</think>')
                    if end > start:
                        content = content[end + 8:].strip()  # 8是</think>的长度
                chat.add_context(content=content, role=msg['role'])
            else:
                chat.add_context(content=msg['content'], role=msg['role'])
        
        if enable_streaming:
            def generate():
                for chunk in chat.ask(prompt):
                    if isinstance(chunk, dict):
                        # 对于结构化的输出直接传递
                        yield f"data: {json.dumps(chunk)}\n\n"
                    else:
                        # 尝试获取推理过程
                        try:
                            if hasattr(chat, 'get_last_reasoning_content'):
                                reasoning = chat.get_last_reasoning_content()
                                if reasoning:
                                    print(f"推理过程: {reasoning}")
                                    yield f"data: {json.dumps({'type': 'reasoning', 'content': reasoning})}\n\n"
                        except Exception as e:
                            print(f"获取推理过程失败: {e}")
                        
                        # 发送实际内容
                        yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
                        print(f"实际内容: {chunk}")
            return Response(generate(), mimetype='text/event-stream')
        else:
            response = chat.ask(prompt)
            result = {'success': True, 'response': response}
            
            # 如果需要包含思考过程
            if include_reasoning and hasattr(chat, 'get_last_reasoning_content'):
                try:
                    reasoning = chat.get_last_reasoning_content()
                    if reasoning:
                        result['reasoning'] = reasoning
                except Exception as e:
                    result['reasoning_error'] = str(e)
            
            return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chain_chat', methods=['GET', 'POST'])
def chain_chat():
    if request.method == 'GET':
        data = request.args
    else:
        data = request.json
        
    query = data.get('query')  # 用户请求
    enable_streaming = data.get('enable_streaming', False)
    use_reasoning_field = data.get('use_reasoning_field', True)  # 是否使用 reasoning_content 字段
    context = data.get('context', [])  # 获取上下文
    
    # 获取推理链配置
    thinking_config = data.get('thinkingConfig', {})
    result_config = data.get('resultConfig', {})
    thinking_prompt = data.get('thinkingPrompt', '')
    result_prompt = data.get('resultPrompt', '')
    
    try:
        # 创建思考阶段的聊天实例
        thinking_chat = AIChat(
            provider=thinking_config.get('modelType'),
            api_key=thinking_config.get('apiKey'),
            model=thinking_config.get('model'),
            enable_streaming=enable_streaming,
            timeout=120
        )
        
        # 创建结果阶段的聊天实例
        result_chat = AIChat(
            provider=result_config.get('modelType'),
            api_key=result_config.get('apiKey'),
            model=result_config.get('model'),
            enable_streaming=enable_streaming,
            timeout=120
        )
        
        # 处理上下文
        for msg in context:
            if msg['role'] == 'assistant':
                content = msg['content']
                if '<think>' in content:
                    start = content.find('<think>')
                    end = content.find('</think>')
                    if end > start:
                        content = content[end + 8:].strip()
                thinking_chat.add_context(content=content, role=msg['role'])
                result_chat.add_context(content=content, role=msg['role'])
            else:
                thinking_chat.add_context(content=msg['content'], role=msg['role'])
                result_chat.add_context(content=msg['content'], role=msg['role'])
        
        if enable_streaming:
            def generate():
                # 思考阶段
                thought_content = []
                thinking_prompt_filled = thinking_prompt.replace('[$query$]', query)
                
                if not use_reasoning_field:
                    yield f"data: {json.dumps({'type': 'content', 'content': '<think>'})}"
                
                for chunk in thinking_chat.ask(thinking_prompt_filled):
                    if isinstance(chunk, dict):
                        content = chunk.get('content')
                        thought_content.append(content)
                        if use_reasoning_field:
                            yield f"data: {json.dumps({'type': 'reasoning', 'content': content})}"
                        else:
                            yield f"data: {json.dumps({'type': 'content', 'content': content})}"
                if not use_reasoning_field:
                    yield f"data: {json.dumps({'type': 'content', 'content': '</think>'})}"
                
                thought = ''.join(thought_content)
                
                # 结果阶段
                result_prompt_filled = result_prompt.replace('[$query$]', query).replace('[$thought$]', thought)
                for chunk in result_chat.ask(result_prompt_filled):
                    if isinstance(chunk, dict):
                        yield f"data: {json.dumps({'type': 'content', 'content': chunk.get('content')})}\n\n"
                        
            return Response(generate(), mimetype='text/event-stream')
        else:
            # 思考阶段
            thinking_prompt_filled = thinking_prompt.replace('[$query$]', query)
            thought = thinking_chat.ask(thinking_prompt_filled)
            if not thought:
                return jsonify({'success': False, 'error': '思考阶段失败'}), 500
                
            # 结果阶段
            result_prompt_filled = result_prompt.replace('[$query$]', query).replace('[$thought$]', thought)
            result = result_chat.ask(result_prompt_filled)
            if not result:
                return jsonify({'success': False, 'error': '结果阶段失败'}), 500
            
            # 构建响应
            response = {
                'success': True,
                'response': result
            }
            
            if use_reasoning_field:
                response['reasoning_content'] = thought
            else:
                response['response'] = f'<think>{thought}</think>{result}'
            
            return jsonify(response)
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def run_server():
    app.run(host='0.0.0.0', port=18000)

if __name__ == '__main__':
    run_server()
