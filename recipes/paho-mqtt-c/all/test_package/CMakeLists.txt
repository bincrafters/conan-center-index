cmake_minimum_required(VERSION 3.15)
project(test_package C)

find_package(eclipse-paho-mqtt-c REQUIRED CONFIG)

if(PAHO_MQTT_C_ASYNC)
    add_executable(${PROJECT_NAME} test_package_async.c)
    if(PAHO_MQTT_C_WITH_SSL)
        if(TARGET eclipse-paho-mqtt-c::paho-mqtt3as)
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3as)
        else()
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3as-static)
        endif()
    else()
        if(TARGET eclipse-paho-mqtt-c::paho-mqtt3a)
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3a)
        else()
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3a-static)
        endif()
    endif()
else()
    add_executable(${PROJECT_NAME} test_package_client.c)
    if(PAHO_MQTT_C_WITH_SSL)
        if(TARGET eclipse-paho-mqtt-c::paho-mqtt3cs)
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3cs)
        else()
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3cs-static)
        endif()
    else()
        if(TARGET eclipse-paho-mqtt-c::paho-mqtt3c)
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3c)
        else()
            target_link_libraries(${PROJECT_NAME} PRIVATE eclipse-paho-mqtt-c::paho-mqtt3c-static)
        endif()
    endif()
endif()
