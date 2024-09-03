docker compose -f docker-compose.yaml up \
                                        --build \
                                        --force-recreate \
                                        --remove-orphans \
                                        --attach image_enhance_service \
                                        --attach broker \
                                        --attach networks \
                                        --attach bot_service
