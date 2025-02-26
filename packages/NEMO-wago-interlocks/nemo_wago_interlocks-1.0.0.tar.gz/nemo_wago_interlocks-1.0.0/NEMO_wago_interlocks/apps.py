from django.apps import AppConfig


class MqttConfig(AppConfig):
    name = "NEMO_wago_interlocks"

    def ready(self):
        from NEMO_wago_interlocks import interlocks  # unused but required import

        pass
