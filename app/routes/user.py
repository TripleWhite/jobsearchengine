from flask import Blueprint, request, jsonify, g
from app.models import User, Job
from app import db
from app.middleware import jwt_required
from app.services.ai_service import parse_resume, match_jobs
from sqlalchemy import or_

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    return jsonify({
        'status': 'ok',
        'user': g.current_user.to_dict()
    })

@bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400

    if 'name' in data:
        g.current_user.name = data['name']
        
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': 'Profile updated'
    })

@bp.route('/update_resume', methods=['PUT'])
@jwt_required
def update_resume():
    data = request.get_json()
    
    if not data or 'resume_text' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Resume text is required'
        }), 400

    # You might want to add a length check here
    if len(data['resume_text']) > 50000:  # Example: limit to 50K characters
        return jsonify({
            'status': 'error',
            'message': 'Resume text exceeds maximum length'
        }), 400

    g.current_user.resume_text = data['resume_text']
    
    try:
        # 解析简历文本
        parsed_data = parse_resume(data['resume_text'])
        g.current_user.set_resume_parsed_data(parsed_data)
        db.session.commit()
        
        return jsonify({
            'status': 'ok',
            'message': 'Resume updated and parsed successfully',
            'parsed_data': parsed_data
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to parse resume: {str(e)}'
        }), 500

@bp.route('/parse_resume', methods=['POST'])
@jwt_required
def parse_current_resume():
    """手动触发简历解析"""
    if not g.current_user.resume_text:
        return jsonify({
            'status': 'error',
            'message': 'No resume text found'
        }), 400

    try:
        parsed_data = parse_resume(g.current_user.resume_text)
        g.current_user.set_resume_parsed_data(parsed_data)
        db.session.commit()
        
        return jsonify({
            'status': 'ok',
            'parsed_data': parsed_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/match_jobs', methods=['GET'])
@jwt_required
def match_jobs_route():
    """职位匹配接口"""
    # 获取查询参数
    desired_position = request.args.get('desired_position')
    desired_location = request.args.get('desired_location')
    
    if not desired_position or not desired_location:
        return jsonify({
            'status': 'error',
            'message': 'Both desired_position and desired_location are required'
        }), 400
    
    # 检查是否有简历数据
    if not g.current_user.resume_text:
        return jsonify({
            'status': 'error',
            'message': 'Please upload your resume first'
        }), 400
    
    # 确保有解析后的简历数据
    resume_parsed_data = g.current_user.get_resume_parsed_data()
    if not resume_parsed_data:
        try:
            resume_parsed_data = parse_resume(g.current_user.resume_text)
            g.current_user.set_resume_parsed_data(resume_parsed_data)
            db.session.commit()
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to parse resume: {str(e)}'
            }), 500
    
    try:
        # 初步筛选职位
        jobs = Job.query.filter(
            or_(
                Job.job_title.ilike(f'%{desired_position}%'),
                Job.location == desired_location
            )
        ).limit(20).all()
        
        if not jobs:
            return jsonify({
                'status': 'ok',
                'recommendations': [],
                'message': 'No matching jobs found'
            })
        
        # 调用职位匹配
        recommendations = match_jobs(
            resume_parsed_data,
            desired_position,
            desired_location,
            [job.to_dict() for job in jobs]
        )
        
        # 获取推荐职位的完整信息
        job_dict = {job.id: job.to_dict() for job in jobs}
        for rec in recommendations:
            job_id = rec['job_id']
            if job_id in job_dict:
                rec['job_details'] = job_dict[job_id]
        
        return jsonify({
            'status': 'ok',
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to match jobs: {str(e)}'
        }), 500
