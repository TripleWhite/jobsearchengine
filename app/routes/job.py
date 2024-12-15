from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Job
from app.middleware import admin_required, jwt_required
from app.services.ai_service import parse_job_description
from datetime import datetime, UTC
import json

bp = Blueprint('job', __name__, url_prefix='/job')

@bp.route('/admin/create_job', methods=['POST', 'OPTIONS'])
@admin_required
def create_job():
    # 明确处理 OPTIONS 请求
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5177'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response, 204
        
    data = request.get_json()
    if not data or 'raw_jd_text' not in data:
        return jsonify({'error': 'Missing raw_jd_text'}), 400

    try:
        # 使用 AI 服务解析 JD
        parsed_data = parse_job_description(data['raw_jd_text'])

        job = Job(
            job_title=parsed_data['job_title'],
            company_name=parsed_data['company_name'],
            location=parsed_data['location'],
            raw_jd_text=data['raw_jd_text']
        )
        job.set_responsibilities(parsed_data['responsibilities'])
        job.set_requirements(parsed_data['requirements'])

        db.session.add(job)
        db.session.commit()

        return jsonify({
            'status': 'ok',
            'job_id': job.id,
            'message': 'Job created successfully',
            'job': job.to_dict()
        }), 201

    except ValueError as e:
        current_app.logger.error(f"Value Error in create_job: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating job: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/', methods=['GET'])
def list_jobs():
    # Get query parameters
    job_title = request.args.get('job_title', '')
    location = request.args.get('location', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Build query
    query = Job.query
    if job_title:
        query = query.filter(Job.job_title.ilike(f'%{job_title}%'))
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))

    # Execute query with pagination
    pagination = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'status': 'ok',
        'jobs': [
            {
                'id': job.id,
                'job_title': job.job_title,
                'company_name': job.company_name,
                'location': job.location,
                'created_at': job.created_at.isoformat()
            }
            for job in pagination.items
        ],
        'pagination': {
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })

@bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({
        'status': 'ok',
        'job': job.to_dict()
    })
