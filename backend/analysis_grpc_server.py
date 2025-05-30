import grpc
from concurrent import futures
import analysis_pb2
import analysis_pb2_grpc
from api.services.analysis_service import analyze_comments_pipeline
from logger import logger


class AnalysisServiceServicer(analysis_pb2_grpc.AnalysisServiceServicer):
    def Analyze(self, request, context):
        logger.info("Step1")
        comments = list(request.comments)
        logger.info(f"Step 1 Comments: {comments}")
        results = analyze_comments_pipeline(comments)
        logger.info(f"Step 1 Results: {comments}")
        topics = []
        for topic_result in results:
            opinions = [
                analysis_pb2.Opinion(type=op["type"], text=op["text"])
                for op in topic_result["opinions"]
            ]
            topics.append(
                analysis_pb2.TopicResult(
                    topic_id=topic_result["topic_id"],
                    topic_summary=topic_result["topic"],
                    opinions=opinions,
                    conclusion=topic_result["conclusion"],
                )
            )
        response = analysis_pb2.AnalyzeResponse(topics=topics)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analysis_pb2_grpc.add_AnalysisServiceServicer_to_server(
        AnalysisServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    print("gRPC server started on port 50051.")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
